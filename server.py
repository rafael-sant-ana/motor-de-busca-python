import os
from math import pow

from flask import Flask, render_template, request

from src.TrieCompacta import TrieCompacta, initialize_index

app = Flask("uai,cade")
trie = TrieCompacta()
FOLDER_PATH = "bbc"
INDEX_FILE = "trie_index.json"
RESULTS_PER_PAGE = 10

initialize_index(trie, FOLDER_PATH, INDEX_FILE)

def search_index(search_term):
    if not search_term:
        return []
    
    search_term = search_term.lower()
    
    node = trie.find(search_term)
    
    if node is None or trie.num_docs == 0:
        return []
    
    results = []
    
    doc_occurrences = [len(val) for val in node.positions.values()]
    
    if not doc_occurrences:
        return []

    avg_occourence = sum(doc_occurrences) / trie.num_docs
    
    if all(count == 0 for count in doc_occurrences):
        std_occourence = 1
    else:
        std_occourence = pow(sum(pow((count - avg_occourence), 2) for count in doc_occurrences) / trie.num_docs, 0.5)

    def calculate_zscore(positions_count):
        if std_occourence == 0:
            return positions_count - avg_occourence
        return (positions_count - avg_occourence) / std_occourence
    
    for path, positions in node.positions.items():
        if positions: 
            count = len(positions)
            zscore = calculate_zscore(count)
            
            results.append({
                'location': path,
                'occurrences': count,
                'zscore': zscore,
                'positions': positions
            })

    results = sorted(results, key=lambda a: a['zscore'], reverse=True)
    
    for res in results:
        try:
            with open(res['location'], "r", encoding="utf-8") as f:
                snippet_text = f.read()
                
            ref_occourence = res['positions'][0]
            
            begin = max(0, ref_occourence - 80)
            end = min(len(snippet_text), ref_occourence + 80)
            
            snippet = snippet_text[begin:end].strip()
            
            highlighted_term = f'<span class="font-semibold bg-yellow-200 p-0.5 rounded-sm">{search_term}</span>'
            res['snippet'] = re.sub(re.escape(search_term), highlighted_term, snippet, flags=re.IGNORECASE)
            
        except Exception as e:
            res['snippet'] = f"Could not read snippet from file: {e}"
            
        del res['zscore']
        del res['positions']
        del res['occurrences']

    return results

@app.route('/')
def home():
    empty_pagination = {'current_page': 0, 'total_pages': 0, 'results_per_page': RESULTS_PER_PAGE, 'total_results': 0}
    return render_template('search_results.html', query=None, results=[], trie=trie, pagination=empty_pagination)

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1 

    all_results = search_index(query)
    total_results = len(all_results)
    
    total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    
    if page < 1: 
        page = 1
    if total_pages > 0 and page > total_pages: 
        page = total_pages
    
    start_index = (page - 1) * RESULTS_PER_PAGE
    end_index = start_index + RESULTS_PER_PAGE
    current_page_results = all_results[start_index:end_index]
    
    pagination_context = {
        'current_page': page,
        'total_pages': total_pages,
        'results_per_page': RESULTS_PER_PAGE,
        'total_results': total_results
    }
    
    return render_template(
        'search_results.html', 
        query=query, 
        results=current_page_results,
        trie=trie, 
        pagination=pagination_context
    )


@app.route('/document/<path:doc_path>')
def view_document(doc_path):
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        filename = os.path.basename(doc_path)

        return render_template('document_view.html', title=filename, content=content, doc_path=doc_path)
    except:
        return "Erro ao abrir arquivo.", 404


if __name__ == '__main__':
    app.run(debug=True)

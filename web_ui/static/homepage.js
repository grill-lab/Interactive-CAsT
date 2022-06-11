var G_activeSearchBar = "#searchbar_hero";
var G_searchButton = "#search_btn_hero"
var G_numDocs = "#num_docs";
var G_passageCount = "#passage_count";
var G_passageSize = "#passage_size";
var G_passageLimit = "#passage_limit";
var G_collection = "#collection";
var G_searcherType = "#searcher_type";
var G_reranker = "#reranker";
var G_rewriter = "#rewriter";
var G_context = "#contextfield_hero";
var G_rawRewriteButton = "#rewrite_raw_btn_hero";
var G_rewriteButton = "#rewrite_btn_hero";
var G_priorTurn = "#prior_turn";
var G_rewriteLogsButton = "#rewrite_logs";
var rewriteLogs = [];
var G_k1 = "#k1_bm25";
var G_b = "#b_bm25"
var G_skip_rerank = "#skip_rerank"


$(G_searchButton).click(function () {
    var searchQuery = $(G_activeSearchBar).val();
    var numDocs = $(G_numDocs).val();
    var passageCount = $(G_passageCount).val();
    var passageSize = $(G_passageSize).val();
    var passageLimit = $(G_passageLimit).val();
    var searcherType = $(G_searcherType).val();
    var collection = $(G_collection).val();
    var reranker = $(G_reranker).val()
    var skipRerank = $(G_skip_rerank).is(':checked').toString();
    var b = $(G_b).val();
    var k1 = $(G_k1).val();

    if (searchQuery == "") {
        alert("There's no content in the Search Bar");
        return;
    }

    searchQuery = searchQuery.replaceAll(" ", "_");
    var url = `/search?query=${searchQuery}&numDocs=${numDocs}
    &passageCount=${passageCount}&passageSize=${passageSize}&passageLimit=${passageLimit}
    &searcherType=${searcherType}&collection=${collection}&reranker=${reranker}
    &skipRerank=${skipRerank}&b=${b}&k1=${k1}`;
    window.location.href = url
});


$(G_rawRewriteButton).click(function () {
    var searchQuery = $(G_activeSearchBar).val();
    var context = $(G_context).val();
    var rewriter = $(G_rewriter).val();
    var prior_turn = "raw"

    requestRewrite(searchQuery, context, rewriter, prior_turn)

});


$(G_rewriteButton).click(function() {
    var searchQuery = $(G_activeSearchBar).val();
    var context = $(G_context).val();
    var rewriter = $(G_rewriter).val();
    var priorTurn = $(G_priorTurn).val();

    requestRewrite(searchQuery, context, rewriter, priorTurn)
});


$(G_rewriteLogsButton).click(function() {
    if (rewriteLogs.length == 0){
        alert("Rewrite a query first!")
    } else {
        var rewrite_logs_csv = convertLogsToCSV(rewriteLogs);
        triggerDownload('.tsv', rewrite_logs_csv)
    }
})


function requestRewrite(searchQuery, context, rewriter, priorTurn) {

    if (searchQuery == "") {
        alert("There's no content in the Search Bar");
        return;
    }

    if (context == ""){
        alert("There is no content in the Context field");
    }

    $.ajax({
        type: "POST",
        url: "rewrite",
        data: JSON.stringify({
            'searchQuery': searchQuery,
            'context' : context,
            'rewriter': rewriter,
            'priorTurn' : priorTurn
        }),
        success: function (results) {
            console.log(results.rewrite);
            rewrittenQuery = results.rewrite;
            $(G_activeSearchBar).val(rewrittenQuery);
            $(G_context).val(results.context)
            
            rewriteLogs.push({
                'query': searchQuery,
                'context': results.context,
                'rewrite': rewrittenQuery
            });
        }
    });


}

function triggerDownload(extension, content) {
    let date = new Date();
    let timestamp = date.getTime();
    let filename = $(G_activeSearchBar).val() + "_" + timestamp + extension;
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}


function convertLogsToCSV(arr) {
    const array = [Object.keys(arr[0])].concat(arr)
  
    return array.map(it => {
        console.log(it)
        return Object.values(it).join('\t')
    }).join('\n')
}

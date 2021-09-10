var G_searchBar = "#searchbar_top"
var G_searchButton = "#search_btn_top"
var G_getTrecEval = "#download_trec_eval"
var G_getSearchResults = "#download_search_results"
var results = JSON.parse($(".pages").attr("results"));
var G_trecEvalResults = [];

$(G_searchButton).click(function () {
    var arguments = window.location.search;
    var argumentsArr = arguments.split("&");
    var searchQuery = $(G_searchBar).val()

    console.log(argumentsArr)
    
    if (searchQuery == "") {
        alert("There's no content in the Search Bar");
        return;
    }

    searchQuery = searchQuery.replaceAll(" ", "_");
    argumentsArr[0] = `query=${searchQuery}`

    var newArguments = argumentsArr.join('&')

    var url = '/search?' + newArguments;
    window.location.href = url
});

function compare( a, b ) {
    if ( a.score > b.score ){
      return -1;
    }
    
    if ( a.score < b.score ){
      return 1;
    }
    
    return 0;
}
  

$(G_getSearchResults).click(function (){
    triggerDownloadJSON(results);
})

$(G_getTrecEval).click(function (){
    G_trecEvalResults = [];

    for (var i = 0; i < results.length; i++){
        //console.log(results[i]["id"]);
        for (var j = 0; j < results[i]["passages"].length; j++){
            G_trecEvalResults.push({
                "query_id": 1,
                "Q0": "Q0",
                "doc_id": results[i]["id"] + ":" + results[i]["passages"][j]["passage_id"],
                "rank": 0,
                "score": results[i]["passages"][j]["score"],
                "run_id": "BASELINE_RUN"
            });
        }
    };

    G_trecEvalResults.sort( compare );

    for (var k = 0; k < G_trecEvalResults.length; k++){
        G_trecEvalResults[k]["rank"] = k + 1;
    }

    triggerDownloadCSV(G_trecEvalResults)
});

function triggerDownload(extension, content) {
    let date = new Date();
    let timestamp = date.getTime();
    let filename = $(G_searchBar).val() + "_" + timestamp + extension;
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function triggerDownloadCSV(results) {
    let csv_content = Papa.unparse(results, {
        quotes: false, //or array of booleans
        quoteChar: '"',
        escapeChar: '"',
        delimiter: ",",
        header: true,
        newline: "\n",
        skipEmptyLines: true, //or 'greedy',
        columns: null //or array of strings
    });
    triggerDownload('.csv', csv_content);
};

function triggerDownloadJSON(results) {
    triggerDownload('.json', JSON.stringify(results));
};

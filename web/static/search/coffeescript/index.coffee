$ ->
  window.filter = "All"
  set_ranker_callbacks()
  $(".input-group").keypress (k) ->
    if k.which == 13 # enter key pressed
      $("#search_button").click()
      return false;
  $("#search_button").click -> do_search()

do_search = () ->
  query = $("#query_text").val()
  if query.length != 0
    $("#search_results_list").empty()
    $.ajax "search-api",
      type: "POST"
      contentType: "application/json; charset=utf-8"
      dataType: "json"
      data: JSON.stringify
        query: query
        filter: window.filter
      success: (data, stat, xhr) -> print_results data
      failure: (axhr, stat, err) ->
        $("#search_results_list").append("<li>Something bad happened!</li>")

set_ranker_callbacks = () ->
  $("#All").click ->
    window.filter = "All"
    $("#search_concept").text("All")
    do_search()
  $("#Courses").click ->
    window.filter = "Courses"
    $("#search_concept").text("Courses")
    do_search()
  $("#News").click ->
    window.filter = "News"
    $("#search_concept").text("News")
    do_search()
  $("#Profiles").click ->
    window.filter = "Profiles"
    $("#search_concept").text("Profiles")
    do_search()

print_results = (result) ->
  console.log result.results
  if result.results.length == 0
    $("#search_results_list").append('<p>No results found!</p>')
    return
  displayed = 0
  for doc in result.results
    break if displayed == 20
    continue if (doc.path.includes ":") or (doc.path.length > 60)
    displayed += 1
    path = doc.name.replace(/_/g, " ")
    html = "<li><h4><a href='#{doc.name}'>#{path}</a>"
    html += "<small class='pull-right'>#{doc.score.toFixed(4)}</small></h4></li>"
    $("#search_results_list").append(html)

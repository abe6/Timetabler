
// Search form handling
// Attach a submit handler to the form
$( "#submitForm" ).submit(function( event ) {
 
    // Stop form from submitting normally
    event.preventDefault();
  
    // Get some values from elements on the page:
    var $form = $(this)
    var url = $form.attr( "action" )
    var formData = {
        "codes" : $form.find( "input[name='codes']" ).val(),
        "semester" : $form.find( "select[name='semester']" ).val()
      };

    // Clear existing content
    $( ".nav-tabs" ).empty()
    $( ".tab-content" ).empty()
    $( ".errors" ).empty()
    // Show loading
    $(` <li class="nav-item">
    <a class="nav-link active" data-toggle="tab" href="#loading">
    Your results are loading... </a></li>`).appendTo('.nav-tabs');
    $(`<div class="tab-pane container active text-center" id="loading"><br>
        <div class="spinner-grow text-muted"></div><br>
        It may take a while to generate the results. Hang in there.  </div>`).appendTo('.tab-content');

    // Send the data using a POST request
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(formData),
      dataType: 'json',
      contentType: "application/json",
    }).done(function (response) {
        // Process response here

        // Empty existing results and add the new ones
        $( ".nav-tabs" ).empty()
        $( ".tab-content" ).empty()
        $( ".errors" ).empty()
        

        // Display code errors
        if(response.invalid.length != 0){
          $(".errors").append(`<p>Invalid unit codes: ${response.invalid.join(", ")}</p>`)
        }
        if(response.notFound.length != 0){
          $(".errors").append(`<p>Units not found running during semester ${formData.semester}: ${response.notFound.join(", ")}</p>`)
        }

        // Handle an empty response
        if(response.results.length == 0){
          $(` <li class="nav-item">
          <a class="nav-link active" data-toggle="tab" href="#error">
          Oh no...</a></li>`).appendTo('.nav-tabs');
          $(`<div class="tab-pane container active text-center" id="error"><br>
          Unable to generate any timetables. Did you select the right semester?</div>`).appendTo('.tab-content');

        } else {
          // Add results
          console.log(response)
          response.results.forEach((result, index) => {
                
            var nextTab = $(".nav-tabs").children().length;

            // create the tab
            $(` <li class="nav-item">
                <a class="nav-link" data-toggle="tab" href="#tab${nextTab}">
                Result ${index+1} </a></li>`).appendTo('.nav-tabs');
        
            // create the tab content
            var content = ""; 
            for (const [day, classes] of Object.entries(result)) {
              content += `<div class="col border border-top-0 border-bottom-0 border-right-0">
                  <h4>${day}</h4>`
              for (const c of classes){
                content += "<p>"+c+"</p>"
              } 
              content += "</div>"
            }
            $(`<div class="tab-pane container fade" id="tab${nextTab}"><br>
                <div class="row mx-1 p-1 text-center"> ${content} </div>
                </div>`).appendTo('.tab-content');
        
            // make the new tab active
            $('#tabs a:last').tab('show');

          });
          $( ".nav-tabs" ).find( "a[href='#tab0']" ).addClass("active")
          $( ".tab-content" ).find( "div[id='tab0']" ).addClass("show active")
        }
    });
  
  });

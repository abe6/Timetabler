
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

    // Clear existing content and show loading
    // TODO:
    $( ".nav-tabs" ).empty()
    $( ".tab-content" ).empty()
    $( ".errors" ).empty()

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
          $(".errors").append(`<p>Unit codes not found: ${response.notFound.join(", ")}</p>`)
        }

        // Handle an empty response
        if(response.results.length == 0){
          console.log("ERROR")
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
            $(`<div class="tab-pane container fade" id="tab${nextTab}">
                ${result.Mon}  </div>`).appendTo('.tab-content');
        
            // make the new tab active
            $('#tabs a:last').tab('show');

          });
          $( ".nav-tabs" ).find( "a[href='#tab0']" ).addClass("active")
          $( ".tab-content" ).find( "div[id='tab0']" ).addClass("show active")
        }
    });
  
  });

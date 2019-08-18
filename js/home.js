
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

    // Clear messages and show loading
    $( ".results" ).empty().append( 
      `<div class="media border rounded-lg p-2 m-3 w-100">
          <div class="spinner-border mr-3 mt-3 rounded-circle align-self-center"></div>
          <div class="media-body">
              <h4>Loading...</h4>
              <p>This may take a moment.</p>
          </div>
      </div>`
    );

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
                
            // Add tab
            $( ".nav-tabs" ).append(`<li class="nav-item">
            <a class="nav-link" role="tab" data-toggle="tab" href="#${index}">Result #${index + 1}</a>
            </li>`)

            // Add content
            $( ".tab-content" ).append(`<div role="tabpanel" class="tab-pane fade" id="${index}"><br><br>
            <p>${result.Mon}    #${index+1}</p>
            </div>`)

          });
          $( ".nav-tabs" ).find( "a[href='#0']" ).addClass("active")
          $( ".tab-content" ).find( "div[id='0']" ).removeClass("fade").addClass("active")
        }
    });
  
  });


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
        $( ".results" ).empty()
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
          $( ".results" ).append( 
            `<div class="media border rounded-lg p-2 m-3 w-100">
                <img src="img/exclamation.png" alt="oops" class="mr-3 mt-3 rounded-circle align-self-top" style="width:60px;">
                  <div class="media-body">
                      <h4>No Results! <small><i class="text-secondary">Sorry.</i></small></h4>
                      <h6>No timetables could be generated.</h6>
                  </div>
              </div>`
          );
        } else {
            response.results.forEach(result => {
                var monday = "";
                for (let i = 0; i < result.Mon.length; i++) {
                  monday = monday + `<p>${result.Mon[i]}</p>`;
                }
                var tuesday = "";
                for (let i = 0; i < result.Tue.length; i++) {
                  tuesday = tuesday + `<p>${result.Tue[i]}</p>`;
                }
                var wednesday = "";
                for (let i = 0; i < result.Wed.length; i++) {
                  wednesday = wednesday + `<p>${result.Wed[i]}</p>`;
                }
                var thursday = "";
                for (let i = 0; i < result.Thu.length; i++) {
                  thursday = thursday + `<p>${result.Thu[i]}</p>`;
                }
                var friday = "";
                for (let i = 0; i < result.Fri.length; i++) {
                  friday = friday + `<p>${result.Fri[i]}</p>`;
                }
                $( ".results" ).append( 
                  `<div class="media border rounded-lg p-2 m-3 answer">
                      <div class="media-body">
                          <h5>MONDAY</h5>
                          ${monday}
                          <h5>TUESDAY</h5>
                          ${tuesday}
                          <h5>WEDNESDAY</h5>
                          ${wednesday}
                          <h5>THURSDAY</h5>
                          ${thursday}
                          <h5>FRIDAY</h5>
                          ${friday}
                      </div>
                  </div>`
                  );
              });
        }
    });
  
  });

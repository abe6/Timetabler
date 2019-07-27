$( document ).ready(function() {

  var entry =  $(".entry");
  entry.clone().appendTo("#searchForm");
  entry.find('.btn-add')
  .removeClass('btn-add').addClass('btn-remove')
  .removeClass('btn-warning').addClass('btn-danger')
  .html('<span> <i class="fas fa-minus my-1"></i> </span>');
  
  setupTimePickers()
});

// Search form handling
// Attach a submit handler to the form
$( "#searchForm" ).submit(function( event ) {
 
    // Stop form from submitting normally
    event.preventDefault();
  
    // Get some values from elements on the page:
    var $form = $(this)
    var url = $form.attr( "action" )
    var data = {
      "classes" : []
    }
      
    // Clear messages and show loading
    $( ".results" ).empty().append( 
        `<div class="media border rounded-lg p-2 mt-3">
            <div class="spinner-border mr-3 mt-3 rounded-circle align-self-center"></div>
            <div class="media-body">
                <h4>Loading...</h4>
                <p>This may take a moment.</p>
            </div>
        </div>`
    );

    // Iterates through all 'class' entries and builds that 'class' object
    $(".entry").each(function() {
      var $entry = $(this);
      var name = $entry.find( "input[name='name']" ).val();
      var type = $entry.find( "select[name='type']" ).val();
      var options = [];

      // Iterates through all 'options' for that class, 
      // builds an 'options' object and adds it to the options array
      $entry.find(".OptionEntry").each(function() {
          var days = $(this).find( "select[name='days']" ).val();
          var start = $(this).find( "input[name='start_time']" ).val();
          var end = $(this).find( "input[name='end_time']" ).val();
          options.push({"days":days, "start":start, "end":end})
      });
      data.classes.push({"name":name, "type":type, "options":options})

    });

    // Send the data using a POST request
    $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify(data),
    dataType: 'json',
    contentType: "application/json; charset=utf-8",
    }).done(function (response) {
        // Process response here
        
        // Empty existing results and add the new ones
        $( ".results" ).empty()

        // Handle a response containing an error
        if(response.error != null){
          $( ".results" ).append(
              `<div class="media border rounded-lg p-2 mt-3">
                <img src="img/exclamation.png" alt="oops" class="mr-3 mt-3 rounded-circle align-self-top" style="width:60px;">
                  <div class="media-body">
                      <h4>ERROR <small><i class="text-secondary">An error has occurred:</i></small></h4>
                      <h6>${response.error}</h6>
                  </div>
              </div>`
          );

        // Handle an empty response
        }else if(response.results.length == 0){
          $( ".results" ).append( 
            `<div class="media border rounded-lg p-2 mt-3">
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
                for (let i = 0; i < result.monday.length; i++) {
                  monday = monday + `<p>${result.monday[i]}</p>`;
                }
                var tuesday = "";
                for (let i = 0; i < result.tuesday.length; i++) {
                  tuesday = tuesday + `<p>${result.tuesday[i]}</p>`;
                }
                var wednesday = "";
                for (let i = 0; i < result.wednesday.length; i++) {
                  wednesday = wednesday + `<p>${result.wednesday[i]}</p>`;
                }
                var thursday = "";
                for (let i = 0; i < result.thursday.length; i++) {
                  thursday = thursday + `<p>${result.thursday[i]}</p>`;
                }
                var friday = "";
                for (let i = 0; i < result.friday.length; i++) {
                  friday = friday + `<p>${result.friday[i]}</p>`;
                }
                $( ".results" ).append( 
                  `<div class="media border rounded-lg p-2 mt-3">
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

// Dynamic form handling
// https://bootsnipp.com/snippets/ykXa
  $(function(){
      $(document).on('click', '.btn-add', function(e){
          e.preventDefault();
  
          var controlForm = $('#searchForm:first'),
              currentEntry = $(this).parents('.entry:first'),
              newEntry = $(currentEntry.clone()).appendTo(controlForm);
  
          newEntry.find('input').val('');
          newEntry.find('.OptionEntry').not('.OptionEntry:first').remove();
          newEntry.find('.OptionEntry .btn-remove2')
            .removeClass('btn-remove2').addClass('btn-add2')
            .removeClass('btn-danger').addClass('btn-warning')
            .html('<span> <i class="fas fa-plus my-1"></i> </span>');

          controlForm.find('.entry:not(:last) .btn-add')
              .removeClass('btn-add').addClass('btn-remove')
              .removeClass('btn-warning').addClass('btn-danger')
              .html('<span> <i class="fas fa-minus my-1"></i> </span>');

          setupTimePickers();
      }).on('click', '.btn-remove', function(e)
      {
          $(this).parents('.entry:first').remove();
  
          e.preventDefault();
          return false;
      });
  });

  $(function(){
    $(document).on('click', '.btn-add2', function(e){
        e.preventDefault();

        var controlForm = $(this).parents('.entry:first'),
            currentEntry = $(this).parents('.OptionEntry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);
          
        newEntry.find('input').not("#startTime").not("#endTime").val('');
        controlForm.find('.OptionEntry:not(:last) .btn-add2')
            .removeClass('btn-add2').addClass('btn-remove2')
            .removeClass('btn-warning').addClass('btn-danger')
            .html('<span> <i class="fas fa-minus my-1"></i> </span>');
        
        setupTimePickers();
    }).on('click', '.btn-remove2', function(e)
    {
        $(this).parents('.OptionEntry:first').remove();

        e.preventDefault();
        return false;
    });
});

function setupTimePickers(){
  $('.clockpicker').clockpicker({
    donetext: 'Confirm',
    placement: 'bottom',
    align: 'left'
});
}
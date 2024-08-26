
 let newElement = document.createElement('div')
 
 $(document).ready( function() {
    $("div").each( function(i) {

     $(this).append("<img src='plates/"+(++i)+".jpg' width='500' height='300' />");

    });
  });

  
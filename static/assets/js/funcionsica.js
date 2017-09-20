function actualiza_municipio( valor ) {
    console.log("Entrando a actualiza_municipio!"); // sanity check

    $.ajax({
        url : "/datosmunicipio", // the endpoint
        type : "GET", // http method
        data : { the_post : valor }, // data sent with the post request
        dataType: "json",
        // handle a successful response
        success : function(data) {
            console.log(data); // another sanity check
            var html = '<option value="">-------------</option>';
            for (var i = 0; i<data.length; i++) {
                html += '<option value="'+data[i].pk+'">'+data[i].fields.nomMunicipio+'</option>';
                console.log(html)
                }
            console.log( 'antes ->  %o ', $('#post-Municipio').html() );
            $('#post-Municipio').html(html);
            console.log( 'despues ->  %o ', $('#post-Municipio').html() );
            },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    }
        });
};


function actualiza_localidad(valor, estado_actual){
    console.log("Entrando actualiza localidad")

    $.ajax({
        url : "/datoslocalidad", // the endpoint
        type : "GET", // http method
        data : { the_post : valor, estado_actual: estado_actual }, // data sent with the post request
        dataType: "json",
        // handle a successful response
        success : function(data) {
            console.log(data); // another sanity check
            var html = '<option value="">-------------</option>';
            for (var i = 0; i<data.length; i++) {
                html += '<option value="'+data[i].pk+'">'+data[i].fields.nomLocalidad+'</option>';
                console.log(html)
                }
            console.log( 'antes ->  %o ', $('#post-Localidad').html() );
            $('#post-Localidad').html(html);
            console.log( 'despues ->  %o ', $('#post-Localidad').html() );
            },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    }
        });
}

$('#post-Estado').on('change',function(event){
    event.preventDefault();
    var valor = $(this).val();
    //console.info('valor: %o', valor);
    //console.info('valor: %O', valor);
    $('#post-Municipio').html('<option value="">-------------</option>');
    console.log("postEstado Cambiado");  // sanity check
    $('#post-Localidad').html('<option value="">-------------</option>');
    actualiza_municipio(valor);
});

$('#post-Municipio').change(function(event){
    event.preventDefault();
    var valor = $(this).val();
    var estado_actual = $('#post-Estado').val();
   $('#post-Localidad').html('<option value="">-------------</option>');


    console.log("Municipio Cambiado")  // sanity check
    actualiza_localidad(valor,estado_actual);
    //create_post();
});

$('#post-Localidad').change(function(event){
    event.preventDefault();
    console.log("Localidad Cambiada")  // sanity check
    //create_post();
});
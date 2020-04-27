$(function(e){
    var controle = true;
    var controle2 = true;
    var captura
    $(".dados").hide();
    $(".dados2").hide();
    $("#listar").click(function(e){
        if (controle == true){
            $(".dados").show();
            controle = false;
        }else{
            $(".dados").hide();
            controle=true;
        }
        captura = $('.total').text()
        //alert($('.dados .table tbody .calculo').text());
    });

    $("#listar2").click(function(e){
        if (controle2 == true){
            $(".dados2").show();
            controle2 = false;
        }else{
            $(".dados2").hide();
            controle2 = true;
        }
     });

    $("#salvar").click(function(e){
        $("#alerta").text("Sucesso!")

    });

});


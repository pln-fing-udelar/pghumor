/**
 * Logica para llamar al servicio del clasificador
 *
 */

 $(document).ready(function(){


    $("#Clasificar").click(function(){

      dataEnviada = {}

      dataEnviada.texto = $("#texto").val();
      $("#Resultado").empty();
      $("#Resultado").prepend('<img style="height:50px;width:50px;margin-bottom:10px;" src="http://hipsterjesus.com/assets/images/ajax_spinner.gif"/>');
      $.ajax({url:"/evaluar",data: dataEnviada, method: "POST",  success:function(result){
        $("#Resultado").empty();
        if (result == 1){
            $("#Resultado").prepend('<div class="alert alert-success" role="alert">El texto ingresado es <strong>Humor</strong></div>');
        }
        if (result == 0){
            $("#Resultado").prepend('<div class="alert alert-danger" role="alert">El texto ingresado <strong>NO</strong> es <strong>Humor</strong></div>');
        }
        //alert(result);
      }
      });

    });


 });
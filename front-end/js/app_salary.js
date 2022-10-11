
const salaryEndpoint = 'https://ijfyj7rryh.execute-api.us-east-1.amazonaws.com/dev/get-salary?';

$('#salaryOfferedQuantityLoader').hide();
$('#salaryOfferedP10Loader').hide();
$('#salaryOfferedP25Loader').hide();
$('#salaryOfferedP50Loader').hide();
$('#salaryOfferedP75Loader').hide();
$('#salaryOfferedP90Loader').hide();
$('#salaryExpectedQuantityLoader').hide();
$('#salaryExpectedP10Loader').hide();
$('#salaryExpectedP25Loader').hide();
$('#salaryExpectedP50Loader').hide();
$('#salaryExpectedP75Loader').hide();
$('#salaryExpectedP90Loader').hide();

function sendSalaryPredictionRequest() {   

    $('#salaryOfferedQuantityGroup').hide();
    $('#salaryOfferedP10Group').hide();
    $('#salaryOfferedP25Group').hide();
    $('#salaryOfferedP50Group').hide();
    $('#salaryOfferedP75Group').hide();
    $('#salaryOfferedP90Group').hide();
    $('#salaryExpectedQuantityGroup').hide();
    $('#salaryExpectedP10Group').hide();
    $('#salaryExpectedP25Group').hide();
    $('#salaryExpectedP50Group').hide();
    $('#salaryExpectedP75Group').hide();
    $('#salaryExpectedP90P50Group').hide();

    $('#salaryOfferedQuantityLoader').show();
    $('#salaryOfferedP10Loader').show();
    $('#salaryOfferedP25Loader').show();
    $('#salaryOfferedP50Loader').show();
    $('#salaryOfferedP75Loader').show();
    $('#salaryOfferedP90Loader').show();
    $('#salaryExpectedQuantityLoader').show();
    $('#salaryExpectedP10Loader').show();
    $('#salaryExpectedP25Loader').show();
    $('#salaryExpectedP50Loader').show();
    $('#salaryExpectedP75Loader').show();
    $('#salaryExpectedP90Loader').show();

    $.ajax(
        {
           type:'GET',
           url: salaryEndpoint,
           data: 'jobCompanyClassification=' + $('#jobCompanyClassification').val()  + '&jobArea=' + $('#jobArea').val()  + '&jobSeniority=' + $('#jobSeniority').val()  + '&jobRole=' + $('#jobRole').val()  + '&jobCoreDevelopmentLanguage=' + $('#jobCoreDevelopmentLanguage').val(),
           success: function(data){                
                $('#salaryOfferedQuantity').val(data.salaryOfferedQuantity);
                $('#salaryOfferedP10').val(data.salaryOfferedP10);
                $('#salaryOfferedP25').val(data.salaryOfferedP25);
                $('#salaryOfferedP50').val(data.salaryOfferedP50);
                $('#salaryOfferedP75').val(data.salaryOfferedP75);
                $('#salaryOfferedP90').val(data.salaryOfferedP90);
                $('#salaryExpectedQuantity').val(data.salaryExpectedQuantity);
                $('#salaryExpectedP10').val(data.salaryExpectedP10);
                $('#salaryExpectedP25').val(data.salaryExpectedP25);
                $('#salaryExpectedP50').val(data.salaryExpectedP50);
                $('#salaryExpectedP75').val(data.salaryExpectedP75);
                $('#salaryExpectedP90').val(data.salaryExpectedP90);
           },
            error: function(error) {
                alert('Não foi possível calcular as faixas de salários. Por favor, verifique se os dados enviados estão corretos');                
            },
            complete: function() {
                $('#salaryOfferedQuantityLoader').hide();
                $('#salaryOfferedP10Loader').hide();
                $('#salaryOfferedP25Loader').hide();
                $('#salaryOfferedP50Loader').hide();
                $('#salaryOfferedP75Loader').hide();
                $('#salaryOfferedP90Loader').hide();
                $('#salaryExpectedQuantityLoader').hide();
                $('#salaryExpectedP10Loader').hide();
                $('#salaryExpectedP25Loader').hide();
                $('#salaryExpectedP50Loader').hide();
                $('#salaryExpectedP75Loader').hide();
                $('#salaryExpectedP90Loader').hide();
                $('#salaryOfferedQuantityGroup').show();
                $('#salaryOfferedP10Group').show();
                $('#salaryOfferedP25Group').show();
                $('#salaryOfferedP50Group').show();
                $('#salaryOfferedP75Group').show();
                $('#salaryOfferedP90Group').show();
                $('#salaryExpectedQuantityGroup').show();
                $('#salaryExpectedP10Group').show();
                $('#salaryExpectedP25Group').show();
                $('#salaryExpectedP50Group').show();
                $('#salaryExpectedP75Group').show();
                $('#salaryExpectedP90P50Group').show();

            }
        }
     );    
};

$('#btnPredictDefault').click(sendSalaryPredictionRequest);

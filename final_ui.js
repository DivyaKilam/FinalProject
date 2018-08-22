//function to set the first item in dropdown list
$(document).ready(function() {
    $('#libraryselector').val(0)
    $('#refgenome').val(0)
    $('#bowtieanalysis').val(0)
})


//function to hide and show upload option to user based on single or paired library selection.
$(document).ready(function() {
    $('#paired').hide()
    $('#pairedselect').click(function()
        {$('#paired').show()
        $('#single').val('')})
    $('#singleselect').click(function()
        {$('#paired').hide()
        $('#single').val('')})
})

//function to hide and show bowtie analysis options.
$(document).ready(function() {
    $('#mode1').hide()
    $('#mode2').hide()
    $('#endtoend').click(function()
        {$('#mode1').show()
        $('#mode2').hide()})
    $('#local').click(function()
        {$('#mode2').show()
        $('#mode1').hide()})
    $('#default').click(function()
        {$('#mode1').hide()
        $('#mode2').hide()})
})
//function to get file name and check file extension
$(document).ready(function() {
    $('input[type="file"]').change(function(e) {
        var fileName = e.target.files[0].name;
        alert('The file"'+fileName+ '" has been selected.');
        //});
        var fileExtension = fileName.split('.').pop();
        var validExtension = 'fq';
        if (fileExtension != validExtension) {
            $('input[type="file"]').val('')
            alert("Invalid file type. Upload file in fastq format");}
        });
});

//function to validate file upload
$(document).ready(function() {
    $('#btnsubmit').click(function()
        {alert("clicked submit")
        if(($('#single').val() == '') || (($('#paired').val() == '') && ($('#libraryselector').val()=='1'))){
            $('#single').val('')
            $('#paired').val('')
            alert("Upload files to check alignment");}
//            return false;
    })
})

// transforms all the form parameters into a string we can send to the server
$(document).ready(function() {
    $('#btnsubmit').click(function() {
//        var encoded=($('#libraryselector').val()+ ($('#refgenome').val())+ ($('#bowtieanalysis').val())+ ($("input[type='radio']:checked").val()));
    alert('start processing');
    //var library=document.getElementById('#libraryselector').value;
    //alert('library');    
    document.getElementById("myForm").submit();

//==$.ajax({
    //==    url:'./final.cgi',
    //==    dataType: 'json',
    //==    method: 'post',
    //==    data: {library:'library'},
    //==    success: function(response) {
    //==        $("#answer").html(response);
    //==    }
    //==});
//   return false;

    //$('#Serialized').text('The Serialized form of input fields is:' + encoded);
    });
});





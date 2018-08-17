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
        {$('#paired').show()})
    $('#singleselect').click(function()
        {$('#paired').hide()})
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


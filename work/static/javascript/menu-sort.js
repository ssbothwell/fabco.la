jQuery(function($) {
    $('.table tbody').sortable({
        axis: "y",
        items: 'tr',
        handle: '.glyphicon-sort',
        update: function(){
            $(this).find('tr').each(function(i) {
                if ($(this).find('input[id$=id]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                }
            });            
        }
    });
    $('.glyphicon-sort').css('cursor', 'move');
});

jQuery(function($) {
    $('.table tbody').sortable({
        items: 'tr',
        handle: '.glyphicon-sort',
        update: function(){
            $(this).find('tr').each(function(i) {
                if ($(this).find('input[id$=name]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                }
            });            
        }
    });
    $('.glyphicon-sort').css('cursor', 'move');
});
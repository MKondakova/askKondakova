$('.js-vote').click(function (ev) {
    ev.preventDefault();

    var $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid');
    $.ajax('/vote/', {
        method: 'POST',
        data: {action: action, qid: qid},
    }).done(function (data) {
        console.log('data: ' + data)
    });
    console.log(action + ' ' + qid)

})
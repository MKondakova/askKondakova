$('.rating').each(function (ev) {
    const rating_field = $(this).find('.rating-field');
    const btns = $(this).find('.js-vote-btn');
    btns.click(function (ev) {
        ev.preventDefault();
        const $this = $(this),
            action = $this.data('action'),
            rate_object_id = $this.data('qid'),
            type = $this.data('type');
        $.ajax('/vote/', {
            method: 'POST',
            data: {action: action, rate_object_id: rate_object_id, type: type},
            dataType: "json",
        }).done(function (data) {
            if (data['redirect']) {
                console.log(data['redirect'])
                window.location = data['redirect'];
            } else {
                if ($this.hasClass('selected')) {
                    $this.removeClass('selected')
                } else {
                    btns.removeClass('selected')
                    $this.addClass('selected')
                }
                rating_field.html(data.qrating);
            }
        });
    });

})
$('.js-correct-input').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        answer_id = $this.data('answerid'),
        question_id = $this.data('questionid');
    $.ajax('/make_correct/', {
        method: 'POST',
        data: {answer_id: answer_id, question_id: question_id},
        dataType: "json",
    }).done(function (data) {
        if (data['redirect']) {
                console.log(data['redirect'])
                window.location = data['redirect'];
            } else {
            showHiddenCheckboxes();
            hideAllImages();
            console.log(this.previousSibling)
            $this.next().addClass('hide')
            $this.prev().removeClass('hide')

        }
    });
});

function showHiddenCheckboxes()
{
    $('label.hide').prop('checked', false).removeClass('hide');
}

function hideAllImages() {
    $('.js-correct-check:not(.hide)').addClass('hide')
}
function changeImage(action) {
    var imgElement = document.getElementsByClassName('teamlogo-image');
    if (action === 'over') {
        imgElement.src = "{{ url_for('static', filename='img/team_logo_white.png') }}";
    } else if (action === 'out') {
        imgElement.src = "{{ url_for('static', filename='img/team_logo.png') }}";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var imgElement = document.getElementById('backImage');
    imgElement.addEventListener('mouseover', function() {
        this.src = "{{ url_for('static', filename='img/service_logo_k.png') }}";
    });
    imgElement.addEventListener('mouseout', function() {
        this.src = "{{ url_for('static', filename='img/service_logo_p.png') }}";
    });
});
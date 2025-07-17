let hamburger = document.querySelector('.nav-hamburger');
hamburger.addEventListener("click", function() {
    document.body.classList.toggle('open');
});




let outline = document.querySelector('.outline');
let cursor = document.querySelector('.cursor');
let links = document.querySelectorAll('a');


document.addEventListener('mousemove', function(e){
    let x = e.clientX;
    let y = e.clientY;

    outline.style.transform = `translate( calc(${x}px - 50%), calc(${y}px - 50%)`;
    cursor.style.transform = `translate( calc(${x}px - 50%), calc(${y}px - 50%)`;
});
links.forEach((link) => {
    link.addEventListener("mouseover", function() {
        outline.classList.add('hover');
        cursor.classList.add('hover');
    });
        link.addEventListener("mouseleave", function() {
            outline.classList.remove('hover');
            cursor.classList.remove('hover');
        });
});

document.addEventListener('DOMContentLoaded', function () {
    const galleryItems = document.querySelectorAll('.gallery-item');

    galleryItems.forEach(function (item, index) {
        item.addEventListener('click', function () {
            createCarouselModal(index);
        });
    });

    function createCarouselModal(startIndex) {
        var strlink="";
        const modal = document.createElement('div');
        modal.classList.add('modal', 'fade');
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-body">
                        <div id="carouselExample" class="carousel slide" data-ride="carousel">
                            <div class="carousel-inner">
                                <!-- Use gallery items as carousel items -->
                                ${Array.from(galleryItems).map((item, index) => `
                                    <div class="carousel-item ${index === startIndex ? 'active' : ''}">
                                        <a href="${ item.getElementsByTagName('img')[0].getAttribute('alt') }"> ${ item.innerHTML }</a>
                                    </div>
                                `).join('')}
                            </div>
                            <a class="carousel-control-prev" href="#carouselExample" role="button" data-slide="prev">
                                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                <span class="sr-only">Previous</span>
                            </a>
                            <a class="carousel-control-next" href="#carouselExample" role="button" data-slide="next">
                                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                <span class="sr-only">Next</span>
                            </a>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Chiudi</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Show modal
        $(modal).modal('show');

        // Remove modal from DOM after it is closed
        $(modal).on('hidden.bs.modal', function () {
            modal.remove();
        });
    }
});


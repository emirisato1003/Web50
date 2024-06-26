const img_box_p_form = document.getElementById('img-box-p-form');
const img_box_i_form = document.getElementById('img-box-i-form');

const p_form = document.getElementById('p-form');

const p_image_id = document.getElementById('id_profile_img');
const i_image_id = document.getElementById('id_icon_img');

const csrf = document.getElementsByName('csrfmiddlewaretoken');

p_image_id.addEventListener("change", () => {
    const img_data = p_image_id.files[0];
    const url = URL.createObjectURL(img_data);
    img_box_p_form.innerHTML = `<img src="${url}" class="d-block w-100 rounded-3" height="200" alt="">`;
});

i_image_id.addEventListener("change", () => {
    const i_img_data = i_image_id.files[0];
    const i_url = URL.createObjectURL(i_img_data);
    img_box_i_form.innerHTML = `<img src="${i_url}" class="d-block w-100 rounded-3" height="200" alt="">`;
});




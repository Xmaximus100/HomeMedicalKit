Dropzone.autoDiscover - false;

const myDropzone = new Dropzone("#my-dropzone", {
    url: "upload/",
    maxFiles: 1,
    acceptedFiles: '.xlsx'
})
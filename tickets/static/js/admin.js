fetch('ateliers', {method: 'GET'})
.then(res => _getData(res, 'json'))
.then(data => {
  console.log(data);
})
.catch(err => {
    console.log(err);
});

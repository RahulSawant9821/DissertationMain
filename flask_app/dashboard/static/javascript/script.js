fetch('http://127.0.0.1:5000/segment_data')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
    // Do something with the data
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

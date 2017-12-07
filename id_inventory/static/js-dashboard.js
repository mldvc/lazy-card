$("document").ready ( function () {

	var endpoint = '/overview/api/chart/data/total/'
	var defaultData = []
	var labels = [];

	$.ajax({
		method: "GET",
		url: endpoint,
		success: function(data) {
			labels = data.labels
			totalData = data.totalData
			successData = data.successData
			spoiledData = data.spoiledData
			typeData = data.typeData
			setTotalChart()
			setSPRChart()
			setSPChart()
			console.log(data)
		},
		error: function(error_data) {
			console.log("error")
			console.log(error_data)
		}
	})

	function setTotalChart() {
		var ctx = document.getElementById("id-total-chart").getContext('2d');
		var myChart = new Chart(ctx, {
		    type: 'bar',
		    data: {
		        labels: labels,
		        datasets: [{
		            label: 'Total prints per Month',
		            data: totalData,
		            backgroundColor: [
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)',
		            	'rgba(54, 162, 235, 0.2)'
		            ],
		            borderColor: [
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)',
		               	'rgba(54, 162, 235, 1)'
		            ],
		            borderWidth: 1,
		        }]
		    },
		    options: {
		        title: {
		            display: true,
		            text: 'Prints per Month',
	                fontColor: "#526f7a",
	                fontSize: 15
		        },
		        legend: {
		        	display: false,
		            labels: {
		                fontColor: "#526f7a",
		                fontSize: 15
		            }
		        },
		        scales: {
		            yAxes: [{
		                ticks: {
		                    beginAtZero:true
		                }
		            }]
		        }
		    }
		});
	}


	function setSPRChart() {
		var ctx = document.getElementById("id-spr-chart").getContext('2d');
		var myChart = new Chart(ctx, {
		    type: 'bar',
		    data: {
		    	labels: ['College', 'High School', 'Elementary', 'Employee', 'Hospital', 'Alumni', 'Plus Card'],
		        datasets: [{
		            label: 'Total prints per ID Type',
		            data: typeData,
		            backgroundColor: [
		                'rgba(255, 99, 132, 0.2)',
		                'rgba(54, 162, 235, 0.2)',
		                'rgba(255, 206, 86, 0.2)',
		                'rgba(75, 192, 192, 0.2)',
		                'rgba(153, 102, 255, 0.2)',
		                'rgba(255, 133, 51, 0.2)',
		                'rgba(255, 153, 255, 0.2)'
		            ],
		            borderColor: [
		                'rgba(255,99,132,1)',
		                'rgba(54, 162, 235, 1)',
		                'rgba(255, 206, 86, 1)',
		                'rgba(75, 192, 192, 1)',
		                'rgba(153, 102, 255, 1)',
		                'rgba(255, 133, 51, 1)',
		                'rgba(255, 153, 255, 1)'
		            ],
		            borderWidth: 1,
		        }]
		    },
		    options: {
		        title: {
		            display: true,
		            text: 'Prints per ID Type',
	                fontColor: "#526f7a",
	                fontSize: 15
		        },
		        legend: {
		        	display: false,
		            labels: {
		                fontColor: "#526f7a",
		                fontSize: 15
		            }
		        },
		        scales: {
		            yAxes: [{
		                ticks: {
		                    beginAtZero:true
		                }
		            }]
		        }
		    }
		});
	}

	function setSPChart() {
		var ctx = document.getElementById("id-sp-chart").getContext('2d');
		var myChart = new Chart(ctx, {
		    type: 'line',
		    data: {
		        labels: labels,
		        datasets: [{
		            label: 'Successful Prints',
		            data: successData,
		            backgroundColor: [
		                'rgba(92, 214, 92, 0.2)'
		            ],
		            borderColor: [
		                'rgba(92, 214, 92, 1)'
		            ],
		            borderWidth: 1,
		            lineTension: 0.3,
		        },
				{
		            label: 'Spoiled Cards',
		            data: spoiledData,
		            backgroundColor: [
		                'rgba(255, 51, 51, 0.2)'
		            ],
		            borderColor: [
		                'rgba(255, 51, 51, 1)'
		            ],
		            borderWidth: 1,
		            lineTension: 0.3,		            
		        }]
		    },
		    options: {
		        title: {
		            display: true,
		            text: 'Successful and spoiled prints per Month',
	                fontColor: "#526f7a",
	                fontSize: 15
		        },
		        legend: {
		            labels: {
		                fontColor: "#526f7a",
		                fontSize: 12
		            }
		        },
		        scales: {
		            yAxes: [{
		                ticks: {
		                    beginAtZero:true
		                }
		            }]
		        }
		    }
		});
	}

})
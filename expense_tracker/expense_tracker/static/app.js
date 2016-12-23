$.ajax({
    url: 'api/list',
    type: 'POST',
    data: {
        item: "Utilities", 
        amount: 42.02,
        paid_to: "Seattle Public Light",
        category: "utilties",
        description: "I need wifi and power"
    },
    success: function(data){
        console.log(data.expenses);
    }
});


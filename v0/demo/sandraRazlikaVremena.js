db.getCollection("post_data").aggregate([
{
         $addFields: {commentSubstring: { $concat: [ "t3_", "$id" ] }}
},
{
        $lookup:
         {
           from:"comment_data",
           localField: "commentSubstring",
           foreignField: "parent_id",
           as: "comments"
         }
    },
    {$unwind:"$comments"},
    {
        $addFields:{
            dateRange: {
                $subtract :[
                {$toDate: { $multiply: [ "$comments.created_utc", 1000 ] } }, 
                { $toDate: { $multiply: [ "$created_utc", 1000 ] }} 
                ]}
        }
    },
    {
        $group:{
            _id: "$id",
            min: {$min: "$dateRange"},
            max: {$max: "$dateRange"},
            minDocument: { $first: { $cond: [{ $eq: ["$dateRange", { $min: "$dateRange" }] }, "$comments", null] } },
            maxDocument: { $first: { $cond: [{ $eq: ["$dateRange", { $max: "$dateRange" }] }, "$comments", null] } } //dodati novo polje
        }
    },
    { $sort: {min: -1} }
    
])
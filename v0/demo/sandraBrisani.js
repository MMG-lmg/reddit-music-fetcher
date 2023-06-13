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
         //izvuci samo od obrisanih autora
        $match: {
            "author": {
                $in: ["[deleted]"]
                //$subtract:["$upvotes", "$downvotes"] : {$gt: 200}
            }
        }
    },
    {
        //racuna razliku izmedju komentara i posta
        $addFields:{
            dateRangeForAuthor: {
                $subtract :[
                {$toDate: { $multiply: [ "$comments.created_utc", 1000 ] } }, 
                { $toDate: { $multiply: [ "$created_utc", 1000 ] }} 
                ]},
           upDownRange: {
               $subtract:["$upvotes", "$downvotes"]
           }
        }
    },
    {
         //izvuci samo gde je razlika veca od 200 izmejdu up i down
        $match: {
                upDownRange : {$gt: 200}
        }
    },
    {
        $group:{
            _id: "$id",
            min: {$min: "$dateRangeForAuthor"},
            max: {$max: "$dateRangeForAuthor"},
            commentText: { $first: { $cond: [{ $eq: ["$dateRangeForAuthor", { $min: "$dateRangeForAuthor" }] }, "$comments.body", null] } }, //dodati novo polje
            score: {$addToSet: "$score"},
            upvotes: {$addToSet: "$upvotes"},
            downvotes: {$addToSet: "$downvotes"}
        }
    },
    { $sort: {max: 1, downvotes: 1} }
    
])
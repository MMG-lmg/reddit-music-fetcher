db.getCollection("post_data").aggregate([
{
         $addFields: {
             dateField: { $toDate: { $multiply: [ "$created_utc", 1000 ] } }
             //totalCoins: { $sum: {$multiply: ["$awards.coin_price", "$awards.count"]} }
             }
         
},
{
        $match: {
            dateField: { $gte: ISODate("2019-01-01"), $lt: ISODate("2023-01-01") },
            total_awards: {$gte: 1}
            
        }
},
    {
        $lookup:
         {
           from:"user_data",
           localField: "author",
           foreignField: "name",
           as: "users"
           
         }
    },
    {
        $unwind: "$users"
    },
    {
        $addFields:{
           upDownRangePost: {
               $subtract:["$upvotes", "$downvotes"]
           },
           totalKarma: "$users.total_karma",
           userCommentKarma: "$users.comment_karma"
        }
    },
    {
        $group:{
            _id: "$id",
            upDownRangePost: {$addToSet: "$upDownRangePost"},
            totalKarma: {$addToSet: "$totalKarma"},
            userCommentKarma: {$addToSet: "$userCommentKarma"},
            percentilleUserCommentKarma: {$addToSet: {$multiply: [{$divide:[ "$totalKarma", "$userCommentKarma"]}, 100]}},
            percentilleTotalPostKarma: {$addToSet: {$multiply: [{$divide:[ "$totalKarma", "$upDownRangePost"]}, 100]}},
            percentilleCommentPostKarma: {$addToSet: {$multiply: [{$divide:[ "$userCommentKarma", "$upDownRangePost"]}, 100]}}
        }
    },
    { $sort: {percentilleCommentPostKarma: 1} }
])
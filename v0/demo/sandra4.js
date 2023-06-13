db.getCollection("comment_data").aggregate([
{
        $lookup:
         {
           from:"user_data",
           localField: "author",
           foreignField: "name",
           as: "user"
           
         }
    },
    {
        $unwind: "$user"
    }, 
    {
       $addFields: {
                dateField: { $toDate: { $multiply: [ "$created_utc", 1000 ] } }
        } 
    },
    {
        $match: {
            dateField: { $gte: ISODate("2020-01-01"), $lt: ISODate("2023-01-01") },
            score: {$gte: 300},
            "user.is_suspended": {$in: [false]}
        }
    },
    {
        //racuna razliku izmedju komentara i posta
        $addFields:{
            totalComments: {
                        $sum: [
                    "$upvotes", "$downvotes"
                    ]
            },
            activityDifference:{
                $abs: {
                    $subtract: [
                        {
                             $sum: [
                    "$upvotes", "$downvotes"
                    ]
                        }, 
                            "$user.total_karma"
                    ]
                }
            }
        }
    },
    {
         $group:{
             _id: "$_id",
             userName:{$addToSet: "$user.name"}, 
             commentText: {$addToSet: "$body"} , //prvi komentar
             totalCommentsActivity: {$addToSet: "$totalComments"},
             totalUserActivity: {$addToSet: "$user.total_karma"},
             activityDifference: {$addToSet: "$activityDifference"}
             
        }
    },
    //{ $sort: {activityDifference: -1, totalUserActivity: 1, totalCommentsActivity: 1} }
])
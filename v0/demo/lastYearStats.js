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
       $addFields: {
                dateField: { $toDate: { $multiply: [ "$created_utc", 1000 ] } }
        } 
    },
    {
        $match: {
            dateField: { $gte: ISODate("2022-01-01"), $lt: ISODate("2023-01-01") }
        }
    },
    {
        $project:{
            _id:0,
            created_utc:0,
            subreddit:0,
            author:0,
            parent_id:0,
            body:0 
        }
    },
    {
        $project:{
            user:{$cond: {
          if: { $eq: [{$size:"$user"}, 0] },
          then: { name: "Removed" },
          else: { $arrayElemAt: [ "$user", 0 ] }
        }},
        _id:0,
        total_awards:1,
        awards:1,
        downvotes:1,
        upvotes:1,
        controversiality:1,
        url:1,
        score:1,
        dateField:1
        }
    },
    {
        $group: {
            _id: "$user.name",
            count: { $sum: 1 },
            total_awards: { $sum: "$total_awards" }, // Calculate the average of another field within the array
            total_score: { $sum: "$score" }, // Find the maximum value of a field within the array
            total_controvertiality:{$sum:"$controversiality"},
            awards: { $push: "$awards" }
        }
    }
])
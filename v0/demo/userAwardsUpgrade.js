db.reformated_posts2.aggregate([
    {
      $project:{
          comments:1
      }  
    },
    {
      $unwind:"$comments"
    },
    {
    $match: {
      "comments.author.name": { $exists: true}
        }
    },
    {
        $unwind:"$comments.awards"
    },
    {
        $group: {
          _id: {
              user:"$comments.author.name",
              awards_name:"$comments.awards.name"
          },
          count: { $sum: 1 },
          days_of_premium:{$sum:{$ifNull: ["$comments.awards.days_of_premium", 0]}},
          coins: {$addToSet:"$comments.awards.coin_price"}
        }  
    },
    {
        $addFields: {
          totalEarnings: { $multiply: ["$count", { $arrayElemAt: ["$coins", 0] }] }
        }
    },
]).explain("executionStats")
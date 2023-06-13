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
    $match: {
      user: { $exists: true, $ne: [] } // Filter documents that have a non-empty arrayField
        }
    },
    {
        $unwind:"$user"
    },
    {
        $unwind:"$awards"
    },
    {
        $group: {
          _id: {
              user:"$user.name",
              awards_name:"$awards.name"
          },
          count: { $sum: 1 },
          days_of_premium:{$sum:{$ifNull: ["$awards.days_of_premium", 0]}},
          coins: {$addToSet:"$awards.coin_price"}
        }  
    },
    {
    $addFields: {
      totalEarnings: { $multiply: ["$count", { $arrayElemAt: ["$coins", 0] }] }
    }
  }
    
])

db.getCollection("post_data").aggregate([
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
        $group:{
            _id:{
                field1:{ $size: "$user"},
                field2: "$user.gold"
            },
            count: { $sum: 1 },
            total_awards: { $sum: "$total_awards" }, 
            total_score: { $sum: "$score" }, 
        }
    }, 
    {
    $project: {
      _id: 0,
      field1:{$cond: {
          if: { $eq: ["$_id.field1", 0] },
          then: "Removed",
          else: "Active"
        }},
      gold:{$cond: {
          if: { $eq: [{$size: "$_id.field2"}, 0] },
          then: false,
          else: { $arrayElemAt: [ "$_id.field2", 0 ] }
        }},
      count: 1,
      total_awards:1,
      total_score:1
    }
  },
  {
     $group:{
            _id:{
                field1:"$field1",
                field2: "$gold"
            }, 
            count: { $sum: "$count" },
            total_awards: { $sum: "$total_awards" }, 
            total_score: { $sum: "$total_score" },
     }
  }   
]).explain("executionStats")

db.getCollection("post_data").aggregate([
    {
         $addFields: {secondSubstring: { $concat: [ "t3_", "$id" ] }}
    },
    {
        $lookup:
         {
           from:"comment_data",
           localField: "secondSubstring",
           foreignField: "parent_id",
           as: "comments"
         }
    },
    {$unwind:"$comments"},
    { $sort: { "comments.score": -1} },
    { $group:{
         _id: "$flair", // Group key
         comments: { $push:"$comments"}
    }},
    {
    $project: {
      _id: 1,
      comments: { $slice: ["$comments", 10] }
    }
  },
    {$unwind:"$comments"},
    
    {
        $lookup:
         {
           from:"user_data",
           localField: "comments.author",
           foreignField: "name",
           as: "user"
         }
    },
    {
    $match: {
      user: { $exists: true, $ne: [] }
        }
    },
    {$unwind:"$user"},
    {
      $addFields: {"comments.scorePerc":{ $cond: [ {$eq:["$user.total_karma", 0]},null, {$multiply: [{$divide:[ "$comments.score", "$user.total_karma"]}, 100]}]}}
    } 
    
])

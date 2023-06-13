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
            "comments.created_date": { $gte: ISODate("2022-01-01"), $lt: ISODate("2023-01-01") }
        }
    },
    {
    $match: {
      "comments.author.id": { $exists: true}
        }
    },
    {
        $group:{
            _id:"$comments.author.name",
            count: { $sum: 1 },
            total_awards: { $sum: "$comments.total_awards" }, // Calculate the average of another field within the array
            total_score: { $sum: "$comments.score" }, // Find the maximum value of a field within the array
            total_controvertiality:{$sum:"$comments.controversiality"},
            awards: { $push: "$comments.awards" }    
        }
    }
]).explain("executionStats")

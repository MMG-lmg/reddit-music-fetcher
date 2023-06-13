db.getCollection("comment_data").aggregate([
        {
            $addFields: {
                deleted: {
                    $cond: { if: { $or: [ { body: "[deleted]" }, { body: "[removed]" } ] }, then: 1, else: 0 }
                },
                secondSubstring: {$arrayElemAt: [{ $split: ["$parent_id", "_"]}, 1]}
            }
        },
        {
            $lookup:
             {
               from:"post_data",
               localField: "secondSubstring",
               foreignField: "id",
               as: "postData"
             }
         },
        {
          $group:
            {
              _id: "$parent_id", // Group key
              total_awards: {$sum:"$total_awards"},
              total_downvotes: {$sum:"$downvotes"},
              total_upvotes: {$sum:"$upvotes"},
              total_score:{$sum:"$score"},
              total_controversial:{$sum:"$controversiality"},
              total_deleted:{$sum:"$deleted"},
            }
        },
        { $sort: { total_controversial: 1,total_deleted : 1, total_score: -1, total_awards: -1 } },
]).explain("executionStats")
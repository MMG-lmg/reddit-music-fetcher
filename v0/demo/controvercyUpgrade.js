db.getCollection("reformated_posts2").aggregate([
    {
      $addFields:
        {
          stats:{
            $reduce: {
                input: "$comments",
                initialValue: { total_awards: 0, total_downvotes: 0, total_upvotes: 0,total_score: 0,total_controversial: 0,total_deleted: 0},
                in: {
                    total_awards: { $add: ["$$value.total_awards", "$$this.total_awards"] },
                    total_downvotes: { $add: ["$$value.total_downvotes", "$$this.downvotes"] },
                    total_upvotes: { $add: ["$$value.total_upvotes", "$$this.upvotes"] },
                    total_score: { $add: ["$$value.total_score", "$$this.score"] },
                    total_controversial: { $add: ["$$value.total_controversial", "$$this.controversiality"] },
                    total_deleted: { $add: ["$$value.total_deleted", {$cond:[{eq:["$$value.body","[deleted]"]},1,0]}] },
                }
            }
          }
        }
    },
    {
      $addFields:{
          "total_awards" :"$stats.total_awards",
          "total_downvotes" :"$stats.total_downvotes",
          "total_upvotes" :"$stats.total_upvotes",
          "total_score" :"$stats.total_controversial",
          "total_controversial" :"$stats.total_controversial",
          "total_deleted" :"$stats.total_deleted",
      }  
    },
    {
       $project:{
           _id:0,
           comments:0,
           stats:0
       }
    }, 
    { $sort: { total_controversial: 1,total_deleted : 1, total_score: -1, total_awards: -1 } },
]).explain("executionStats")

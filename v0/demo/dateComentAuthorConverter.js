db.reformated_posts2.aggregate([
  {
    $addFields: {
      comments: {
        $map: {
          input: "$comments", //created_date: { $toDate: "$$item.created_utc" },
          as: "item",
          in: {
              $cond: [
              { $eq: [{ $type: "$$item.author" }, "object"] },
                {$mergeObjects: [
                  "$$item",
                  {
                    author:{
                        $mergeObjects:[
                        "$$item.author",
                        {
                            created_date: { $toDate: "$$item.author.created_utc" },
                        }
                        ]
                    }    
                  }
                ]
              },
          "$$item" // Skip conversion for string author
          ]
          }
        }
      }
    }
  },
  {
    $out: "reformated_posts2"
  }
])
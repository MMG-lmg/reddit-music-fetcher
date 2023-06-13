db.reformated_posts2.aggregate([
  {
    $addFields: {
      comments: {
        $map: {
          input: "$comments",
          as: "item",
          in: {
            $mergeObjects: [
              "$$item",
              {
                created_date: { $toDate: "$$item.created_utc" }
              }
            ]
          }
        }
      }
    }
  },
  {
    $addFields: {
      "comments.created_utc": "$$REMOVE"
    }
  },
  {
    $out: "reformated_posts2"
  }
])
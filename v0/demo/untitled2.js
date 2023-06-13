db.getCollection("comment_data").aggregate([
    {
        $match:{
            author:"Badman_Battle"
        }
    },
    {
        $addFields: {
          secondSubstring: { $arrayElemAt: [{ $split: ["$parent_id", "_"] }, 1] }
        }
    },
    {$lookup:
         {
           from:"comment_data",
           localField: "secondSubstring",
           foreignField: "id",
           as: "resultingArray"
         }
     },
     { $unwind: "$resultingArray"}
])
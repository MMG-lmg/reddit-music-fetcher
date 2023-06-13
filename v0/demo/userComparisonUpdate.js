db.getCollection("reformated_posts2").aggregate([

    {
        $match: {
            "created_date": { $gte: ISODate("2022-01-01"), $lt: ISODate("2023-01-01") }
        }
    },
    {
        $group:{
            _id:{
                field1: {$eq:["$author.name","[deleted]"]},
                field2: {$ifNull: ["$author.gold",false]}
            },
            count: { $sum: 1 },
            total_awards: { $sum: "$total_awards" }, 
            total_score: { $sum: "$score" }, 
        }
    },
    {
        $project:{
            _id:0,
            suspended:"$_id.field1",
            is_premium:"$_id.field2",
            count:1,
            total_awards:1,
            total_score:1
        }
    }
]).explain("executionStats")

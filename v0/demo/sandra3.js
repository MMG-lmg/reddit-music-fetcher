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
        $unwind: "$user"
    },
    {
        $match: {
                "user.verified" : {$in:[true]}  //samo verifikovani nalozi
        }
    },
    {
        $addFields: {
                dateFieldComment: { $toDate: { $multiply: [ "$created_utc", 1000 ] } }, //kad je nastao komentar
                dateFieldUser: { $toDate: { $multiply: [ "$user.created_utc", 1000 ] } }, //kad je nastao user,
                dateRangeForAuthorComment: {
                $subtract :[
                {$toDate: { $multiply: [ "$user.created_utc", 1000 ] } }, 
                { $toDate: { $multiply: [ "$created_utc", 1000 ] }} 
                ]},
                totalLinkedKarmaDifference: { 
                    $abs: {
                        $subtract: [
                    "$user.total_karma", "$user.linked_karma"
                    ]
                    }
                },
                awarderAwardedKarmaDifference: { 
                    $abs: {
                        $subtract: [
                    "$user.awarder_karma", "$user.awarded_karma"
                    ]
                    }
                },
                upDownCommentDifference: {
                    $abs: {
                        $subtract: [
                    "$upvotes", "$downvotes"
                    ]
                    }
                },
                /*userName: {
                    "$user.name"
                }*/
                    
        } 
    },
    {
        $group:{
             _id: "$user.id",
             dateUserCommentDifference: {$min: "$dateRangeForAuthorComment"}, //prvi komentar
             totalLinkedKarmaDifference: {$addToSet: "$totalLinkedKarmaDifference"},
             awarderAwardedKarmaDifference: {$addToSet: "$awarderAwardedKarmaDifference"},
             upDownCommentDifference:  {$addToSet: "$upDownCommentDifference"},
             userName:{$addToSet: "$user.name"},
             commentText: { $first: { $cond: [{ $eq: ["$dateRangeForAuthorComment", { $min: "$dateRangeForAuthorComment" }] }, "$comments.body", null] } },
        }
    },
    { $sort: {dateuserCommentDifference: -1, updownCommentDifference: 1} }
    
    
])
db.getCollection("reformated_posts2").aggregate([
    {
        $project:{
            "comments.score":1,
            "comments.author":1,
            "comments.flair":"$flair"
        }
    },
    {$unwind:"$comments"},
    { $sort: { "comments.flair":1, "comments.score": -1} },
    { $group:{
         _id: "$comments.flair", // Group key
         comments:{
             $accumulator: {
              init: function() {
                return [];
              },
              accumulateArgs: ["$comments"],
              accumulate: function(state, currentField) {
                if (state.length < 10) {
                  state.push(currentField);
                }
                return state;
              },
              merge: function(state1, state2) {
                return state1.concat(state2).sort((a, b) => b.score - a.score ).slice(0, 10);
              },
              lang: "js"
            }
         }
    }},
    {$unwind:"$comments"},
    {
        $addFields: {"comments.scorePerc":{ $cond: [ {$eq:["$comments.author.total_karma", 0]},null, {$multiply: [{$divide:[ "$comments.score", "$comments.author.total_karma"]}, 100]}]}} 
    }
]).explain("executionStats")

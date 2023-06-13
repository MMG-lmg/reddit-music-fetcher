db.reformated_posts2.aggregate([
  {
    $addFields: {
      created_date: {
        $toDate: "$created_utc"
      }
    }
  },
  {
    $addFields: {
        "author.created_date": {
        $toDate: "$author.created_utc"
        }
    }
  },
  
  {
    $out: "reformated_posts2"
  }
])

// Update the collection with the modified documents
db.reformated_posts2.bulkWrite([
  {
    updateMany: {
      filter: {},
      update: { $unset: {created_utc:"","author.created_utc":""} }
    }
  }
])
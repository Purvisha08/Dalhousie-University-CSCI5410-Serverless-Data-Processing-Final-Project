
import AWS from 'aws-sdk'
import { ItemList } from 'aws-sdk/clients/dynamodb';

const S3_BUCKET ='food-recipes-server';
const REGION = process.env.REACT_APP_AWS_REGION;
const AWS_ACCESS_KEY = process.env.REACT_APP_AWS_ACCESS_KEY
const AWS_SECRET_ACCESS_KEY = process.env.REACT_APP_AWS_SECRET_ACCESS_KEY
const AWS_ACCESS_TOKEN = process.env.REACT_APP_AWS_ACCESS_TOKEN

const TABLE_NAME = "Recipe"

// https://www.telerik.com/kendo-react-ui/components/cloud/amazon-dynamo-db/

AWS.config.update({
    region: REGION,
    accessKeyId: AWS_ACCESS_KEY,
    secretAccessKey: AWS_SECRET_ACCESS_KEY,
    // sessionToken: AWS_ACCESS_TOKEN
})

// https://medium.com/bb-tutorials-and-thoughts/how-to-make-api-calls-in-react-applications-7758052bf69

// AWS.config.update({
//     region: 'us-east-1',
//     accessKeyId: 'ASIA5ILWA2XJOZATJXMW',
//     secretAccessKey: '1gJfE0eskjoy4k0pmeqKmDc/0OHXr98Ze+AQQosB',
//     sessionToken: 'FwoGZXIvYXdzEIz//////////wEaDMsMskpWcA41MFgdxiLAAd8c7ISj5mlBGFWtGiI9MENuG6C5LO2VjIypZAOr6Bv8cwdwRgLrvQw/jaG8WnrUbc+ga03GvoV1u6JIkrAcON0BZK7iuyIj8ecbWA4b+LVAcHLbSfKRbeguD2+ni9+jcXp+52W3mRW4wb1EY7c40l4n3JbPVc5WUM+5TT/3zqDHhCFsflw/ebFJTvVzyR3d8ehRYzbh9gs+mh4oCIElV6Tp/tJuD8XjWEYAzTGr+0aFV8jmY+gboasuk+5/QyPTlSjW0+ubBjItNdQofDVJ7ZebUWPsdj88+xGEgeSdAErIJEQwh+xULYYVBwcEMSoYLvzywk3k'
// })

const uploadRecipe = (file) => {

    const myBucket = new AWS.S3({
        params: { Bucket: S3_BUCKET},
        region: REGION,
    })

    const params = {
        ACL: 'public-read',
        Body: file,
        Bucket: S3_BUCKET,
        Key: file.name
    };

    myBucket.putObject(params)
        .on('httpUploadProgress', (evt) => {
            console.log("file uploading")
        })
        .send((err) => {
            if (err) console.log(err)
        })
}

const putRecipeData = (data) => {

    const docClient = new AWS.DynamoDB.DocumentClient()
    var params = {
        TableName: TABLE_NAME,
        Item: data
    }

    console.log(params)
    
    docClient.put(params, function (err, data) {
        if (err) {
            console.log('Error', err)
        } else {
            console.log('Success', data)
        }
    })
}

const fetchRecipeData = async () => {

    const docClient = new AWS.DynamoDB.DocumentClient()
    var params = {
        TableName: TABLE_NAME
    }

    let output = [];

    const items = await docClient.scan(params).promise();

    items.Items?.map((d) => {
        output.push({
            id: d.receipeId,
            name: d.recipeName,
            fileName: d.fileName,
            rastaurantId: d.restaurantId,
            price: d.price
        })
    })

    return output


}

const extractData = async (recipe) => {

    const requestOptions = {
        method: 'POST',
        body: JSON.stringify(recipe)
    }

    const response = await fetch("https://octsgfp6fgkw7yd644nrbstot40tqdqi.lambda-url.us-east-1.on.aws/", requestOptions)
        .then(response => response.json()).then(data => alert("exraction done"))

}

const updateRecipe = async (id, fileName) => {

    const docClient = new AWS.DynamoDB.DocumentClient()

    let params = {
        TableName: TABLE_NAME,
        Key:{
            "receipeId": id
        },
    UpdateExpression: "set fileName= :fileName",
    ExpressionAttributeValues: { ":fileName": fileName},
    };
    docClient.update(params, function(err, data) {
        if (err) {
            console.log(err);
        } else {
            console.log("data updated")
        }
    });
}

export {
    uploadRecipe,
    putRecipeData,
    fetchRecipeData,
    extractData,
    updateRecipe
}
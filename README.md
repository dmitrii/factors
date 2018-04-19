# factors
AppScale/AppEngine demo app that calculates prime factors of an integer

*Optional:* To build the Angular-based Web app for a front-end,
install `npm` and `ng` and do this in the `angular` directory:

```
npm install
ng build
cp dist/* ../dist
```

To test the application on App Engine with a *development server*, 
install Google Cloud SDK and deploy with:

```
dev_appserver.py . factoring_service
```

To run the application on *AppScale*, add the AppScalefile to the
top directory and deploy with:

```
appscale deploy --project factors .
appscale deploy --project factors factoring_service/
```

To run the application on *Google App Engine*, be sure to select
the project with GAE enabled and deploy with:

```
gcloud app deploy . factoring_service
```

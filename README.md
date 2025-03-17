# qdebc-pr2-spotify

This project aims to build a robust data infrastructure capable of handling, processing, storing, and generating reports from large volumes of real-time data for a company similar to Spotify. The infrastructure will support high-throughput data ingestion, real-time processing, efficient storage, and seamless reporting capabilities.

### Deploy
To deploy it, run the following command in the directory where the yml file is located:

```console
docker-composev -f [docker-compose-file.yml] up -d
```

### Catalog
* `redpanda console`: **http://localhost:8081**.
* `kafka ui`: **http://localhost:8082**.
* `Hadoop Namenode`: **http://localhost:9870/dfshealth.html#tab-overview**
* `Hadoop History server`: **http://localhost:8188/applicationhistory**
* `Hadoop Datanode`: **http://localhost:9864/**
* `Hadoop Nodemanager`: **http://localhost:8042/node**
* `Hadoop Resource manager`: **http://localhost:8088/**

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Contact
For any questions or suggestions, please reach out to our team.

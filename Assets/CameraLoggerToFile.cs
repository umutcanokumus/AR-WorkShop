using System.IO;
using UnityEngine;

public class CameraLoggerToFile : MonoBehaviour
{
    public GameObject trackedObject;        // Takip edilen obje (örn. küp)
    public Transform playspaceTransform;    // Playspace (MixedRealityPlayspace)

    private string filePath;
    private StreamWriter writer;

    private float logInterval = 0.1f;
    private float timeSinceLastLog = 0f;

    private float initialDistance = -1f;

    void Start()
    {
        filePath = Path.Combine(Application.persistentDataPath, "DistanceLog.csv");
        writer = new StreamWriter(filePath, false);

        // Başlık satırı
        writer.WriteLine("Time,ObjectX,ObjectY,ObjectZ,CameraX,CameraY,CameraZ,Distance,DeltaDistance,InitialDistance");

        Debug.Log("Logger başlatıldı: " + filePath);
    }

    void Update()
    {
        timeSinceLastLog += Time.deltaTime;

        if (timeSinceLastLog >= logInterval)
        {
            LogData();
            timeSinceLastLog = 0f;
        }
    }

    void LogData()
    {
        if (trackedObject == null || playspaceTransform == null)
            return;

        Vector3 objPos = trackedObject.transform.position;
        Vector3 camPos = Camera.main.transform.position;

        float distance = Vector3.Distance(objPos, camPos);

        if (initialDistance < 0f)
        {
            initialDistance = distance;
        }

        float deltaDistance = distance - initialDistance;
        float time = Time.time;

        string line = string.Format("{0:F2},{1:F4},{2:F4},{3:F4},{4:F4},{5:F4},{6:F4},{7:F4},{8:F4},{9:F4}",
            time,
            objPos.x, objPos.y, objPos.z,
            camPos.x, camPos.y, camPos.z,
            distance,
            deltaDistance,
            initialDistance);

        writer.WriteLine(line);
    }

    private void OnApplicationQuit()
    {
        if (writer != null)
        {
            writer.Flush();
            writer.Close();
            Debug.Log("Kayıt tamamlandı ve kapatıldı.");
        }
    }
}

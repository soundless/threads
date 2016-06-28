/**
 * Created by hengjuntian on 6/6/16.
 */
public class SynchronizedCounter {
    long count = 0;

    public void inc() {
        synchronized (this) {
            count++;
        }
    }

    public long count() {
        synchronized (this) {
            return this.count;
        }
    }
}

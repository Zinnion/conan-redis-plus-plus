#include <sw/redis++/redis++.h>
#include <iostream>
using namespace sw::redis;

int main(int argc, char **argv)
{

    auto redis = Redis("tcp://127.0.0.1");

    // Redis class doesn't have built-in *CLIENT SETNAME* method.
    // However, you can use Redis::command to send the command manually.
    redis.command<void>("client", "setname", "name");
    auto val = redis.command<OptionalString>("client", "getname");
    if (val)
    {
        std::cout << *val << std::endl;
    }

    // NOTE: the following code is for example only. In fact, Redis has built-in
    // methods for the following commands.

    // Arguments of the command can be strings.
    // NOTE: for SET command, the return value is NOT always void, I'll explain latter.
    redis.command<void>("set", "key", "100");

    // Arguments of the command can be a combination of strings and integers.
    auto num = redis.command<long long>("incrby", "key", 1);

    // Argument can also be double.
    auto real = redis.command<double>("incrbyfloat", "key", 2.3);

    // Even the key of the command can be of arithmetic type.
    redis.command<void>("set", 100, "value");

    val = redis.command<OptionalString>("get", 100);

    // If the command returns an array of elements.
    std::vector<OptionalString> result;
    redis.command("mget", "k1", "k2", "k3", std::back_inserter(result));

    // Or just parse it into a vector.
    result = redis.command<std::vector<OptionalString>>("mget", "k1", "k2", "k3");

    // Arguments of the command can be a range of strings.
    auto set_cmd_strs = {"set", "key", "value"};
    redis.command<void>(set_cmd_strs.begin(), set_cmd_strs.end());

    auto get_cmd_strs = {"get", "key"};
    val = redis.command<OptionalString>(get_cmd_strs.begin(), get_cmd_strs.end());

    // If it returns an array of elements.
    result.clear();
    auto mget_cmd_strs = {"mget", "key1", "key2"};
    redis.command(mget_cmd_strs.begin(), mget_cmd_strs.end(), std::back_inserter(result));

    return 0;
}
